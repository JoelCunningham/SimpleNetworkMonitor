import { ViewOwnerButtons } from '#components/buttons';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('ViewOwnerButtons', () => {
  let component: ViewOwnerButtons;
  let fixture: ComponentFixture<ViewOwnerButtons>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewOwnerButtons],
    }).compileComponents();

    fixture = TestBed.createComponent(ViewOwnerButtons);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
