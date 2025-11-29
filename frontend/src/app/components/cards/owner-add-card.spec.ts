import { OwnerAddCard } from '#components/cards';
import { provideHttpClient } from '@angular/common/http';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('OwnerAddCard', () => {
  let component: OwnerAddCard;
  let fixture: ComponentFixture<OwnerAddCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OwnerAddCard],
      providers: [provideHttpClient()],
    }).compileComponents();

    fixture = TestBed.createComponent(OwnerAddCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
