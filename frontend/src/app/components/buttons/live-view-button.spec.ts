import { LiveViewButton } from '#components/buttons';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('LiveViewButton', () => {
  let component: LiveViewButton;
  let fixture: ComponentFixture<LiveViewButton>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LiveViewButton],
    }).compileComponents();

    fixture = TestBed.createComponent(LiveViewButton);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
