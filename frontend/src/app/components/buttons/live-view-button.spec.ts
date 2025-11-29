import { LiveViewButton } from '#components/buttons';
import { provideHttpClient } from '@angular/common/http';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('LiveViewButton', () => {
  let component: LiveViewButton;
  let fixture: ComponentFixture<LiveViewButton>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LiveViewButton],
      providers: [provideHttpClient()],
    }).compileComponents();

    fixture = TestBed.createComponent(LiveViewButton);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
